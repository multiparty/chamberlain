import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CardinalsPage } from './cardinals.page';

const routes: Routes = [
  {
    path: '',
    component: CardinalsPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class CardinalsPageRoutingModule {}
