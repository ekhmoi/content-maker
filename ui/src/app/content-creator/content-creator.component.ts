import {
  AfterContentInit,
  AfterViewInit,
  Component,
  OnInit,
  ViewChild,
} from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { WebsocketService } from '../websocker.service';
import { filter } from 'rxjs';
import { MATERIAL_COMPONENTS } from '../material.components';
import { MatStepper, MatStepperModule } from '@angular/material/stepper';
import { MatToolbarModule } from '@angular/material/toolbar';
import { DomSanitizer } from '@angular/platform-browser';
import { FormControl, FormGroup, Validators } from '@angular/forms';

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
export class ContentCreatorComponent implements OnInit, AfterViewInit {
  step1Control = new FormGroup({
    formCtrl: new FormControl('', [Validators.required]),
  });
  step2Control = new FormGroup({
    formCtrl: new FormControl('', [Validators.required]),
  });
  step3Control = new FormGroup({
    formCtrl: new FormControl('', [Validators.required]),
  });
  step4Control = new FormGroup({
    formCtrl: new FormControl('', [Validators.required]),
  });
  step5Control = new FormGroup({
    formCtrl: new FormControl('', [Validators.required]),
  });
  step6Control = new FormGroup({
    formCtrl: new FormControl('', [Validators.required]),
  });

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
    private router: Router,
    private ws: WebsocketService,
    private sanitizer: DomSanitizer
  ) {}

  ngAfterViewInit(): void {
    setTimeout(() => {
      const step = +(this.route.snapshot.queryParamMap.get('step') || '0');
      this.stepper.selectedIndex = step;
      this.stepper.selectionChange.subscribe((val) => {
        console.log('Next value', val);
        this.router.navigate(['.'], {relativeTo: this.route, queryParams: {step: val.selectedIndex}, replaceUrl: true})
      });
    }, 50);
  }

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
        const orderedStepName = [
          'input',
          'audio_transcriber_result',
          'text_analyzer_result',
          'script_generator_result',
          'image_describer_result',
          'image_generator_result',
        ];
        this.running = false;
        this.details[orderedStepName[this.stepper.selectedIndex]] = res;
      });
    }
  }

  saveChanges() {
    const updates = Object.entries(this.details)
      .filter(([key, value]) => this.originalDetails[key] !== value)
      .map(([key, content]) => ({ file_name: `${key}.txt`, content }));
    this.ws.send('update_content_details', { folder_name: this.id, updates });
  }

  onNextClick() {
    const step = this.stepper.selectedIndex + 1;
    this.stepper.next();
    this.executeStep(step);
  }

  executeStep(step = this.stepper.selectedIndex) {
    this.running = true;
    this.ws.send('execute_content_step', {
      step: step,
      folder_name: this.id,
    });
  }
}
