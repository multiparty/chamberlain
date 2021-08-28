import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { AnalyticsPageRoutingModule } from './analytics-routing.module';

import { AnalyticsPage } from './analytics.page';
import { NgxDatatableModule } from "@swimlane/ngx-datatable";

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    AnalyticsPageRoutingModule,
    NgxDatatableModule
  ],
  declarations: [AnalyticsPage]
})
export class AnalyticsPageModule {}
