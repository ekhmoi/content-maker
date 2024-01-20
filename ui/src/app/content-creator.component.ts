import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { WebsocketService } from './websocker.service';
import { filter } from 'rxjs';
import { MATERIAL_COMPONENTS } from './material.components';
import { MatStepperModule } from '@angular/material/stepper';
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
        <button mat-icon-button>
          <mat-icon>play_arrow</mat-icon>
        </button>
        <button mat-icon-button>
          <mat-icon>pause</mat-icon>
        </button>
      </div>
    </mat-toolbar>
    <mat-stepper [linear]="false" #stepper [animationDuration]="'0'">
      <mat-step label="Converting">
        <div>
          <button mat-button matStepperNext>Next</button>
        </div>
      </mat-step>
      <mat-step label="Transcribing">
        <mat-form-field>
          <mat-label>Transcription</mat-label>
          <textarea
            matInput
            [value]="details.audio_transcriber_result"
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button matStepperNext>Next</button>
        </div>
      </mat-step>
      <mat-step label="Analysing">
        <mat-form-field>
          <mat-label>Analysis</mat-label>
          <textarea
            matInput
            [value]="
              details.transcription_analyzer_result ||
              details.text_analyzer_result
            "
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button matStepperNext>Next</button>
        </div>
      </mat-step>
      <mat-step label="Scripting">
        <mat-form-field>
          <mat-label>Script</mat-label>
          <textarea
            matInput
            [value]="details.script_generator_result"
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button matStepperNext>Next</button>
        </div>
      </mat-step>
      <mat-step label="Imagining">
        <mat-form-field>
          <mat-label>Image Descriptions</mat-label>
          <textarea
            matInput
            [value]="details.image_describer_result"
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button matStepperNext>Next</button>
        </div>
      </mat-step>
      <mat-step label="Drawing">
        <mat-form-field>
          <mat-label>Images</mat-label>
          <textarea
            matInput
            [value]="details.image_generator_result"
          ></textarea>
        </mat-form-field>
        <div>
          <button mat-button matStepperPrevious>Back</button>
          <button mat-button matStepperNext>Next</button>
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
  details!: any;
  isLinear = false;

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
        });
      this.ws.open.pipe(filter((open) => !!open)).subscribe(() => {
        this.ws.send('get_content_details', this.id);
      });
    }
  }
}
