import { NgModule } from '@angular/core';
import { RouterModule, Routes,ParamMap } from '@angular/router';
import{IndexComponent}from './Home/index/index.component';
import{PlaylistComponent}from './Home/playlist/playlist.component'
const routes: Routes = [
  { path: 'index', component:PlaylistComponent },
  {path:'playlist',component:IndexComponent},
  {path:'',component:PlaylistComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
