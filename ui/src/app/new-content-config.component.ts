import { Component, OnInit } from '@angular/core';
import { MATERIAL_COMPONENTS } from './material.components';
import { CommonModule } from '@angular/common';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';

import { FormControl, FormGroup } from '@angular/forms';

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
        <mat-form-field appearance="outline">
          <mat-label>Prompt</mat-label>
          <textarea
            style="min-height: 12rem"
            type="input"
            matInput
            placeholder="You can improve result by providing key points to focus for example"
          ></textarea>
        </mat-form-field>
        <mat-slide-toggle formControlName="pauseAfterEachStep">
          Pause after each step
        </mat-slide-toggle>
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
    input: new FormControl(''),
    pauseAfterEachStep: new FormControl(false),
  });
  constructor(private dialogRef: MatDialogRef<NewContentConfigComponent>) {}

  ngOnInit() {}

  start() {
    this.dialogRef.close(this.form.value);
  }
}
