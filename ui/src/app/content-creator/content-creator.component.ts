import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { WebsocketService } from '../websocker.service';
import { filter } from 'rxjs';
import { MATERIAL_COMPONENTS } from '../material.components';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { MatToolbarModule } from '@angular/material/toolbar';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-content-creator',
  templateUrl: './content-creator.component.html',
  styleUrls: ['./content-creator.component.scss'],
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

  get youtubeURL() {
    return this.sanitizer.bypassSecurityTrustResourceUrl(
      'http://www.youtube.com/embed/' +
        this.id +
        '?enablejsapi=1&origin=http://localhost:4200'
    );
  }

  constructor(
    private route: ActivatedRoute,
    private ws: WebsocketService,
    private sanitizer: DomSanitizer
  ) {}

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

      this.ws.on('execute_content_step_result').subscribe((res) => {
        console.log('execute_content_step_result', res);
        const orderedStepName = [
          'input',
          'audio_transcriber_result',
          'text_analyzer_result',
          'script_generator_result',
          'image_describer_result',
          'image_generator_result',
        ];
        this.running = false;
        this.details[orderedStepName[this.stepper.selectedIndex + 1]] = res;
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
    this.running = true;
    console.log(this.stepper);
    const step = this.stepper.selectedIndex + 1;
    this.stepper.next();
    this.ws.send('execute_content_step', {
      step: step,
      folder_name: this.id,
    });
  }
}
