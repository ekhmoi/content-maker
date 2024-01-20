import { Routes } from '@angular/router';
import { ContentListComponent } from './content-list.component';
import { ContentCreatorComponent } from './content-creator.component';

export const routes: Routes = [
  { path: '', component: ContentListComponent },
  { path: 'new', component: ContentCreatorComponent },
  { path: 'details/:id', component: ContentCreatorComponent },
];
