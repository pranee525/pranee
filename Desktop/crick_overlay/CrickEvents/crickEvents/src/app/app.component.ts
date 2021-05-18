import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'crickEvents';
  images:string[]=[];
  ngonInit(){
    this.images = [ "https://picsum.photos/id/944/900/500","https://picsum.photos/id/1011/900/500","https://picsum.photos/id/984/900/500"]
  }
}

