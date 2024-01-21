import { Component, OnInit } from '@angular/core';
import { MATERIAL_COMPONENTS } from './material.components';
import { MatDialogRef } from '@angular/material/dialog';

import { FormControl, FormGroup } from '@angular/forms';
import { WebsocketService } from './websocker.service';
import { switchMap, tap } from 'rxjs';

@Component({
  selector: 'app-new-content-config',
  template: `
    <h1 mat-dialog-title>New Content</h1>
    <div mat-dialog-content>
      To start creating your next awesome content provide some initial data.
      <form
        [formGroup]="form"
        style="display: flex; flex-direction: column; width: 100%; margin-top: 1rem"
      >
        <mat-form-field appearance="outline">
          <mat-label>Title</mat-label>
          <input
            type="text"
            matInput
            formControlName="title"
            placeholder="Name your new content"
          />
        </mat-form-field>
        <mat-form-field appearance="outline">
          <mat-label>Youtube URL</mat-label>
          <input
            type="text"
            matInput
            formControlName="input"
            placeholder="Youtube URL"
          />
        </mat-form-field>
        <p style="text-align: center">or</p>
        <mat-form-field appearance="outline">
          <mat-label>Drop a file</mat-label>
          <input type="input" matInput placeholder="Drop your file here" />
        </mat-form-field>
        <mat-slide-toggle
          formControlName="automaticSteps"
          style="margin: 1rem 0"
        >
          Automatically continue after each step
        </mat-slide-toggle>
        <mat-form-field appearance="outline">
          <mat-label>Prompt</mat-label>
          <textarea
            style="min-height: 12rem"
            type="input"
            matInput
            placeholder="You can improve result by providing key points to focus for example"
          ></textarea>
        </mat-form-field>
      </form>
    </div>
    <div mat-dialog-actions style="justify-content: flex-end">
      <button mat-button mat-dialog-close>Cancel</button>
      <button mat-raised-button color="primary" (click)="start()">Start</button>
    </div>
  `,
  standalone: true,
  imports: [...MATERIAL_COMPONENTS],
})
export class NewContentConfigComponent implements OnInit {
  form = new FormGroup({
    title: new FormControl(''),
    input: new FormControl(''),
    automaticSteps: new FormControl(true),
  });
  constructor(
    private dialogRef: MatDialogRef<NewContentConfigComponent>,
    private ws: WebsocketService
  ) {}

  ngOnInit() {}

  start() {
    this.ws.send('download_content_from_youtube', {
      folder_name: this.form.value.title,
      youtube_url: this.form.value.input,
    });
    this.ws
      .once('download_content_from_youtube_result')
      .pipe(
        tap(() => {
          this.ws.send('execute_content_step', {
            step: 0,
            folder_name: this.form.value.title,
          });
        }),
        switchMap(() => this.ws.once('execute_content_step_result'))
      )
      .subscribe((res) => {
        console.log('Got new content', res);

        this.dialogRef.close(true);
      });
  }
}
