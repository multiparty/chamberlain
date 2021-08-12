import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { WorkflowsPage } from './workflows.page';

const routes: Routes = [
  {
    path: '',
    component: WorkflowsPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class WorkflowsPageRoutingModule {}
