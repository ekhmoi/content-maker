import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  EMPTY,
  Observable,
  Subject,
  filter,
  map,
  take,
} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class WebsocketService {
  open = new BehaviorSubject(false);
  private socket!: WebSocket;
  listener: Subject<any> = new Subject();

  public connect(url: string): Subject<any> {
    if (!this.socket || this.socket.readyState === WebSocket.CLOSED) {
      this.socket = new WebSocket(url);

      this.socket.onmessage = (event) => {
        console.log('Returning data', event.data);
        let data = event.data;
        try {
          data = JSON.parse(data);
        } catch (err) {
          console.log('Could not parse result as json');
        }
        this.listener.next(data);
      };
      this.socket.onopen = (ev) => {
        console.log('Socket opened', ev);
        if (this.open.getValue() === false) {
          this.open.next(true);
        }
      };

      this.socket.onerror = (event) => {
        // Handle error
        console.error('WebSocket error:', event);
      };
    }
    return this.listener;
  }

  public once(command: string) {
    return this.on(command).pipe(take(1));
  }

  public on(command: string) {
    return this.listener.pipe(
      filter((message) => message.command === command),
      map(({ data }) => data)
    );
  }

  public send(command: string, data: any, stream = false) {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ command, data }));
      return stream
        ? this.on(`${command}_result`)
        : this.once(`${command}_result`);
    } else {
      console.error('WebSocket connection is not open.');
      return EMPTY;
    }
  }

  public close(): void {
    if (this.socket) {
      this.socket.close();
    }
  }
}
