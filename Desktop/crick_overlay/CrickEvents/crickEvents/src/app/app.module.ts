import { NgModule,NO_ERRORS_SCHEMA,CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { IndexComponent } from './Home/index/index.component';
import { PlaylistComponent } from './Home/playlist/playlist.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {IvyCarouselModule} from 'angular-responsive-carousel';
import {CommonModule}from '@angular/common';
import {HttpClientModule}from'@angular/common/http';
import { NgxYoutubePlayerModule } from 'ngx-youtube-player';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';




@NgModule({
  declarations: [
    AppComponent,
    IndexComponent,
    PlaylistComponent,
    
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    IvyCarouselModule,
    CommonModule,
    HttpClientModule,
    NgxYoutubePlayerModule,
    
  ],
  providers: [],
  bootstrap: [AppComponent],schemas: [
    CUSTOM_ELEMENTS_SCHEMA,
    NO_ERRORS_SCHEMA
  ]
})
export class AppModule { }
