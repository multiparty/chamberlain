import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ComputePage } from './compute.page';

const routes: Routes = [
  {
    path: '',
    component: ComputePage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ComputePageRoutingModule {}
