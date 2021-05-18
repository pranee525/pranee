import { Component, OnInit } from '@angular/core';

import { ActivatedRoute } from '@angular/router';
import { HttpClient } from "@angular/common/http";
import { DomSanitizer } from '@angular/platform-browser';
import { NumberSymbol } from '@angular/common';
import{NgxYoutubePlayerModule} from 'ngx-youtube-player';


export interface videoInfo {
  videoId:number,
  src:string,
  title:string,
  matchId:number,
  matchType:string,
  showOnTop:boolean,
  img:string

}
@Component({
  selector: 'app-playlist',
  templateUrl: './playlist.component.html',
  styleUrls: ['./playlist.component.css']
})
export class PlaylistComponent implements OnInit {

  name="";
  topSafeUrl="";
  topVideo:videoInfo={matchId:0,matchType:"",videoId:0,src:"",showOnTop:false,title:"",img:""};
  otherVideos:Array<videoInfo>=[];
  
  public player:any;
   id: string = 'qDuKsiwS5xw';
 
  constructor(private httpClient:HttpClient,private _sanitizer:DomSanitizer) { }

  ngOnInit(): void {

    this.httpClient.get("/assets/js/liveMatches.json").subscribe(data =>{
      console.log(data);
      console.log(data["matchInfo"].length)

      for(var i=0;i<data["matchInfo"].length;i++){
        if(data["matchInfo"][i].showOnTop){
          this.topVideo=data["matchInfo"][i];
        }
        else{
          this.otherVideos.push(data["matchInfo"][i]);
        }

      }

      
     this.topSafeUrl==this._sanitizer.bypassSecurityTrustUrl(this.topVideo.src)
      console.log(this.topVideo)
      console.log(this.otherVideos)
      //this.products = data;
    })
  }

  videoURL(url:string) {
    return this._sanitizer.bypassSecurityTrustResourceUrl(url);
  }


  savePlayer(player) {
    this.player = player;
  
    console.log('player instance', player);
  }
  onStateChange(event) {
    console.log('player state', event.data);
    console.log(this.player.getVolume())
    console.log(this.player.getOptions())

  
  }


}
