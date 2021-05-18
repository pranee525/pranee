import { Component, OnInit,NO_ERRORS_SCHEMA,CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';
import { NgImageSliderComponent } from 'ng-image-slider';
import {CommonModule} from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from "@angular/common/http";
import { DomSanitizer } from '@angular/platform-browser';


export interface videoInfo_index {
  videoId:number,
  src:string,
  title:string,
  matchId:number,
  matchType:string,
  showOnTop:boolean,
  img:string,
  index:number

}

import {IvyCarouselModule} from 'angular-responsive-carousel';
import { videoInfo } from '../playlist/playlist.component';
@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.css']
})
export class IndexComponent implements OnInit {
   
   match=0;
   videoId=0;
   isInit:boolean=true;
   
  topVideo:videoInfo_index={matchId:0,matchType:"",videoId:0,src:"",showOnTop:false,title:"",img:"",index:0};
  innings_1:Array<videoInfo_index>=[];
  innings_2:Array<videoInfo_index>=[];
  liveVideo:videoInfo_index={matchId:0,matchType:"",videoId:0,src:"",showOnTop:false,title:"",img:"",index:0};
  
  constructor(private route: ActivatedRoute,private httpClient: HttpClient,private _sanitizer:DomSanitizer) { }

  ngOnInit(): void {
    console.log("Came here to check data")
    this.route.queryParams.subscribe(params => {
      this.match = params['matchId']!=null?params["matchId"]:0;
      this.videoId=params['videoId'];

    });
    if(this.isInit){
      this.loadVideos(this.match,this.videoId);
      this.isInit=false;
    }
    else{
      this.swapVideos(this.match,this.videoId);
    }
    
    
  }

  loadVideos(selectedMatchId:number,selectedVideoId:number){
    console.log(this.match+"matchId true")
    this.httpClient.get("/assets/js/liveMatches.json").subscribe(data =>{
      console.log(data +"this info");
      console.log(data["matchInfo"].length)
      var arr_selected=data["matchInfo"].find(el=>el.matchId==this.match)
      console.log("found the array")
      console.log(arr_selected)
      if(this.liveVideo.videoId==0)
      {
        this.liveVideo.videoId=arr_selected.videoId;
        this.liveVideo.title=arr_selected.title;
        this.liveVideo.src=arr_selected.src;
        this.liveVideo.matchType=arr_selected.matchType;
        this.liveVideo.matchId=arr_selected.matchId;

      }
      var inning_1_info=arr_selected.videos.innings_1;
      var inning_2_info=arr_selected.videos.innings_2;
      this.innings_1=[];
      this.innings_2=[];
      for(var i=0;i<inning_1_info.length;i++){
        if(inning_1_info[i].videoId==this.videoId)
        {
          this.topVideo=inning_1_info[i];

          this.innings_1.push(this.liveVideo)
        }
        else{
        this.innings_1.push(inning_1_info[i])
        }

      }
      for(var i=0;i<inning_2_info.length;i++){

        if(inning_2_info[i].videoId==this.videoId)
        {
          this.topVideo=inning_2_info[i];
          this.innings_2.push(this.liveVideo)
        }
        else{
        this.innings_2.push(inning_2_info[i])
        }
      }

      if(this.topVideo.videoId===0){
        this.topVideo=this.liveVideo;
      }
console.log(this.innings_1)
console.log(this.innings_2)
      //this.products = data;
    })

  }
  swapVideos(selectedMatchId:number,selectedVideoId:number){
      console.log("comes here now");
  }

  videoURL(url:string) {
    return this._sanitizer.bypassSecurityTrustResourceUrl(url);
  }


}
