import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ContentCreatorService {
  config: any;

  constructor() {}

  setConfig(config: any) {
    console.log('Setting config', config);
    this.config = config;
  }
}
