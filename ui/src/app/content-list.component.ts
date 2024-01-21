import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { MATERIAL_COMPONENTS } from './material.components';
import { Router, RouterModule } from '@angular/router';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { NewContentConfigComponent } from './new-content-config.component';
import { ContentCreatorService } from './content-creator.service';
import { WebsocketService } from './websocker.service';
import { filter, take, tap } from 'rxjs';

@Component({
  selector: 'app-content-list',
  standalone: true,
  imports: [...MATERIAL_COMPONENTS, RouterModule],
  styles: [
    `
      :host {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
      }
      .content-card {
        min-width: 15rem;
        padding: 0.5rem;
        margin: 1rem;
      }
    `,
  ],
  template: `
    <button
      mat-raised-button
      color="primary"
      (click)="newContent()"
      style="height: 200px; width: 200px; margin: 2rem 2rem;"
    >
      <!-- New Content -->
      <mat-icon style="font-size: 5rem;height: 5rem; width: 5rem;">
        add
      </mat-icon>
    </button>
    <mat-card *ngFor="let content of contents" class="content-card">
      <mat-card-header>
        <!-- <div mat-card-avatar class="example-header-image"></div> -->
        <mat-card-title>{{ content.folder_name }}</mat-card-title>
        <!-- <mat-card-subtitle>Dog Breed</mat-card-subtitle> -->
      </mat-card-header>
      <!-- <img
        mat-card-image
        src="https://material.angular.io/assets/img/examples/shiba2.jpg"
        alt="Photo of a Shiba Inu"
      /> -->
      <mat-card-content>
        <ul>
          <li *ngFor="let file of content.file_names">{{ file }}</li>
          <!-- {{ content.file_names.join(', ') }} -->
        </ul>
      </mat-card-content>
      <mat-card-actions style="justify-content: space-between">
        <button mat-button (click)="deleteContent(content.folder_name)">
          Delete
        </button>
        <button
          mat-raised-button
          color="primary"
          [routerLink]="['/details', content.folder_name]"
        >
          View
        </button>
      </mat-card-actions>
    </mat-card>
  `,
})
export class ContentListComponent implements OnInit {
  contents: { file_names: string[]; folder_name: string }[] = [];
  constructor(
    private router: Router,
    private dialog: MatDialog,
    private ws: WebsocketService,
    private service: ContentCreatorService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.refresh();
    this.ws.on('get_contents_result').subscribe((data) => {
      this.contents = data;
      this.cdr.detectChanges();
    });
  }

  refresh() {
    this.ws.open
      .pipe(
        filter((open) => !!open),
        take(1)
      )
      .subscribe(() => this.ws.send('get_contents', {}));
  }

  newContent() {
    const dialog = this.dialog.open(NewContentConfigComponent, {
      width: '550px',
    });

    dialog.afterClosed().subscribe((res) => {
      if (res) {
        // this.service.setConfig(res);
        // this.router.navigate(['/new']);
        setTimeout(() => {
          this.refresh();
        }, 200)
      }
    });
  }

  deleteContent(name: string) {
    if (!confirm('Action is irrevertable. Delete content - ' + name + '?')) return;

    this.ws.send('delete_content', { folder_name: name });
    this.ws.once('delete_content_result').subscribe(() => this.refresh());
  }
}
