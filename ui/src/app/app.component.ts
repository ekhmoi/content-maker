import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ContentListComponent } from './content-list.component';
import { WebsocketService } from './websocker.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, ContentListComponent],
  template: '<router-outlet></router-outlet>',
})
export class AppComponent {
  wsURI = 'ws://localhost:6789'
  wsSubscription!: Subscription;
  constructor(private websocketService: WebsocketService) {
    this.wsSubscription = this.websocketService
      .connect(this.wsURI)
      .subscribe(
        (message) => {
          console.log('Received message:', message.command);
        },
        (error) => console.error(error),
        () => console.log('WebSocket connection completed')
      );
  }

  ngOnDestroy() {
    this.wsSubscription.unsubscribe();
    this.websocketService.close();
  }
}
