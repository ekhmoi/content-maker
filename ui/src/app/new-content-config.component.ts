import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { MATERIAL_COMPONENTS } from './material.components';
import { MatDialogRef } from '@angular/material/dialog';

import { FormControl, FormGroup } from '@angular/forms';
import { WebsocketService } from './websocker.service';
import {
  Subscription,
  debounce,
  debounceTime,
  filter,
  switchMap,
  tap,
} from 'rxjs';

@Component({
  selector: 'app-new-content-config',
  template: `
    <h1 mat-dialog-title>New Content</h1>

    <div mat-dialog-content>
      <ng-container *ngIf="!loading && !created">
        <p>
          To start creating your next awesome content provide some initial data.
        </p>
        <form
          [formGroup]="form"
          style="display: flex; flex-direction: column; width: 100%; margin-top: 1rem"
        >
          <mat-form-field appearance="outline">
            <mat-label>Youtube URL</mat-label>
            <input
              type="text"
              matInput
              formControlName="input"
              placeholder="Youtube URL"
            />
          </mat-form-field>

          <mat-form-field appearance="outline">
            <mat-label>ID</mat-label>
            <input
              type="text"
              matInput
              formControlName="ID"
              placeholder="Content ID"
            />
          </mat-form-field>
          <!-- <p style="text-align: center">or</p>
          <mat-form-field appearance="outline">
            <mat-label>Drop a file</mat-label>
            <input type="input" matInput placeholder="Drop your file here" />
          </mat-form-field> -->
          <mat-slide-toggle
            formControlName="automaticSteps"
            style="margin: 1rem 0"
          >
            Automatically continue after each step
          </mat-slide-toggle>
          <mat-form-field appearance="outline">
            <mat-label>Prompt</mat-label>
            <textarea
              style="min-height: 8rem"
              type="input"
              matInput
              formControlName="prompt"
              placeholder="You can improve result by providing key points to focus for example"
            ></textarea>
          </mat-form-field>
        </form>
      </ng-container>

      <ng-container *ngIf="created">
        <p>
          Youtube content has been downloaded and converted. Ready for the next
          steps?
        </p>
      </ng-container>

      <div *ngIf="loading || created">
        <ng-container *ngIf="!created">
          <p>Processing input video...</p>
        </ng-container>
        <div class="progress-messages">
          <div class="message" *ngFor="let message of currentMessages">
            {{ message }}
          </div>
        </div>
      </div>
    </div>
    <div
      mat-dialog-actions
      style="justify-content: flex-end"
      *ngIf="!loading && !created"
    >
      <button mat-button mat-dialog-close>Cancel</button>
      <button mat-raised-button color="primary" (click)="start()">
        Start Creating
      </button>
    </div>

    <div mat-dialog-actions style="justify-content: flex-end" *ngIf="created">
      <button mat-button mat-dialog-close>Create another</button>
      <button mat-raised-button color="primary" (click)="goToNewContent()">
        Continue
      </button>
    </div>
  `,
  styles: [
    `
      .progress-messages {
        background: #0000002e;
        width: calc(100% - 2rem);
        padding: 0.75rem 1rem;
        border-radius: 7px;
        font-style: italic;
        line-height: 35px;
        box-shadow: inset 0px 0px 5px 0px rgb(0 0 0 / 41%);
        height: 80px;
        overflow-x: hidden;
        overflow-y: scroll;
      }
    `,
  ],
  standalone: true,
  imports: [...MATERIAL_COMPONENTS],
})
export class NewContentConfigComponent implements OnInit, OnDestroy {
  loading = false;
  created = false;
  result: any;
  currentLoadingStep: string = '';
  subs: Subscription[] = [];
  currentMessages: string[] = [
    `[${new Date().toJSON().substr(11, 8)}] Initialized new folder.`,
  ];
  messages: { [key: string]: string } = {
    download_video_start: 'Started to download video...',
    download_video_end: 'Video download completed.',
    convert_to_wav_start: 'Started converting to WAV...',
    convert_to_wav_end: 'Conversion to WAV completed.',
    convert_local_file_start: 'Reducing file size...',
    convert_local_file_end: 'Reducing file size completed.',
  };
  form = new FormGroup({
    ID: new FormControl(''),
    input: new FormControl(''),
    automaticSteps: new FormControl({ value: false, disabled: true }),
    prompt: new FormControl({value: '', disabled: true}),
  });

  constructor(
    private dialogRef: MatDialogRef<NewContentConfigComponent>,
    private ws: WebsocketService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.form.controls.input.valueChanges.pipe(debounceTime(300)).subscribe(input => {
      const url = new URL(input as string);
      const id = url.searchParams.get('v')
      this.form.controls.ID.setValue(id);
      this.cdr.detectChanges();
    })
  }

  ngOnDestroy() {
    this.subs.forEach((sub) => sub?.unsubscribe());
  }

  start() {
    this.form.disable();
    this.loading = true;
    this.ws.send('execute_content_step', {
      step: 0,
      folder_name: this.form.value.ID,
      input: this.form.value.input,
    });
    this.ws.once('execute_content_step_result').subscribe((res) => {
      this.result = res;
      console.log('Got res', this.result);
    });
    const supportedCommands = Object.keys(this.messages);
    this.subs.push(
      this.ws.listener
        .pipe(
          // debounceTime(1000),
          filter((message) => supportedCommands.includes(message.command))
        )
        .subscribe(({ command }) => {
          this.currentMessages.unshift(
            `[${new Date().toJSON().substr(11, 8)}] ${this.messages[command]}`
          );

          if (command === 'convert_local_file_end') {
            this.created = true;
            this.loading = false;
          }
          this.cdr.detectChanges();
        })
    );
  }

  goToNewContent() {
    this.dialogRef.close(
      this.result?.split('outputs/')?.[1]?.split('/input.wav')?.[0]
    );
  }
}
