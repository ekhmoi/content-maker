import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { WebsocketService } from './websocker.service';
import { filter } from 'rxjs';
import { MATERIAL_COMPONENTS } from './material.components';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-content-creator',
  styles: [
    `
      mat-toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        span {
          display: inherit;
          align-items: center;
        }
      }

      mat-form-field {
        width: 100%;
      }

      textarea {
        min-height: calc(100vh - 300px) !important;
      }
    `,
  ],
  template: ` <mat-toolbar>
      <span>
        <button mat-icon-button routerLink="/">
          <mat-icon>home</mat-icon>
        </button>
        {{ id || 'New Content' }}
      </span>
      <div class="buttons">
        <button mat-icon-button *ngIf="!running">
          <mat-icon>play_arrow</mat-icon>
        </button>
        <button mat-icon-button *ngIf="running">
          <mat-icon>pause</mat-icon>
        </button>
        <button mat-icon-button *ngIf="!editing" (click)="editing = true">
          <mat-icon>edit</mat-icon>
        </button>
        <button mat-icon-button *ngIf="editing" (click)="saveChanges()">
          <mat-icon>save</mat-icon>
        </button>
      </div>
    </mat-toolbar>
    <mat-stepper #stepper [linear]="false" [animationDuration]="'0'">
      <mat-step label="Converting">
        <div>
          <button mat-button (click)="executeStep()">Next</button>
        </div>
      </mat-step>
      <mat-step label="Transcribing">
        <mat-form-field>
          <mat-label>Transcription</mat-label>
          <textarea
            [readonly]="!editing"
            [disabled]="running"
            matInput
            [(ngModel)]="details.audio_transcriber_result"
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button (click)="executeStep()">Next</button>
        </div>
      </mat-step>
      <mat-step label="Analysing">
        <mat-form-field>
          <mat-label>Analysis</mat-label>
          <textarea
            [readonly]="!editing"
            [disabled]="running"
            matInput
            [(ngModel)]="details.text_analyzer_result"
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button (click)="executeStep()">Next</button>
        </div>
      </mat-step>
      <mat-step label="Scripting">
        <mat-form-field>
          <mat-label>Script</mat-label>
          <textarea
            [readonly]="!editing"
            [disabled]="running"
            matInput
            [(ngModel)]="details.script_generator_result"
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button (click)="executeStep()">Next</button>
        </div>
      </mat-step>
      <mat-step label="Imagining">
        <mat-form-field>
          <mat-label>Image Descriptions</mat-label>
          <textarea
            [readonly]="!editing"
            [disabled]="running"
            matInput
            [(ngModel)]="details.image_describer_result"
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button (click)="executeStep()">Next</button>
        </div>
      </mat-step>
      <mat-step label="Drawing">
        <mat-form-field>
          <mat-label>Images</mat-label>
          <textarea
            [readonly]="!editing"
            [disabled]="running"
            matInput
            [(ngModel)]="details.image_generator_result"
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button (click)="executeStep()">Next</button>
        </div>
      </mat-step>
      <mat-step>
        <ng-template matStepLabel>Done</ng-template>
        <p>You are now done.</p>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button (click)="stepper.reset()">Reset</button>
        </div>
      </mat-step>
    </mat-stepper>`,
  standalone: true,
  imports: [
    ...MATERIAL_COMPONENTS,
    MatStepperModule,
    MatToolbarModule,
    RouterModule,
  ],
})
export class ContentCreatorComponent implements OnInit {
  id!: string;
  originalDetails!: any;
  details!: any;
  editing = false;
  running = false;
  isLinear = false;

  @ViewChild('stepper') stepper!: MatStepper;

  constructor(private route: ActivatedRoute, private ws: WebsocketService) {}

  ngOnInit() {
    if (this.route.snapshot.paramMap.has('id')) {
      this.id = this.route.snapshot.paramMap.get('id') || '';
      this.ws.listener
        .pipe(
          filter((message) => message.command === 'get_content_details_result')
        )
        .subscribe(({ data }) => {
          this.details = Object.entries(data).reduce(
            (remapped, [key, value]) => ({
              ...remapped,
              [key.split('.')[0]]: value,
            }),
            {} as any
          );
          this.originalDetails = JSON.parse(JSON.stringify(this.details));
        });
      this.ws.open.pipe(filter((open) => !!open)).subscribe(() => {
        this.ws.send('get_content_details', this.id);
      });
    }
  }

  saveChanges() {
    const updates = Object.entries(this.details)
      .filter(([key, value]) => this.originalDetails[key] !== value)
      .map(([key, content]) => ({ file_name: `${key}.txt`, content }));
    this.ws.send('update_content_details', { folder_name: this.id, updates });
  }

  executeStep() {
    console.log(this.stepper);
    const step = this.stepper.selectedIndex + 1;
    this.ws.send('execute_content_step', {
      step: step,
      folder_name: this.id,
    });
  }
}
