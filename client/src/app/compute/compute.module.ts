import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ComputePageRoutingModule } from './compute-routing.module';

import { ComputePage } from './compute.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ComputePageRoutingModule
  ],
  declarations: [ComputePage]
})
export class ComputePageModule {}
