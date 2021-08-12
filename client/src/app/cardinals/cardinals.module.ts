import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { CardinalsPageRoutingModule } from './cardinals-routing.module';

import { CardinalsPage } from './cardinals.page';
import { NgxDatatableModule } from '@swimlane/ngx-datatable';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    CardinalsPageRoutingModule,
    NgxDatatableModule
  ],
  declarations: [CardinalsPage]
})
export class CardinalsPageModule {}
