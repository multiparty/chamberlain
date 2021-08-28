import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { DatasetsPageRoutingModule } from './datasets-routing.module';

import { DatasetsPage } from './datasets.page';
import { NgxDatatableModule } from '@swimlane/ngx-datatable';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    DatasetsPageRoutingModule,
    NgxDatatableModule
  ],
  declarations: [
    DatasetsPage
  ]
})
export class DatasetsPageModule {}
