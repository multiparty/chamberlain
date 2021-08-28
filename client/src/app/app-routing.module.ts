import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'datasets',
    pathMatch: 'full'
  },
  {
    path: 'folder/:id',
    loadChildren: () => import('./folder/folder.module').then( m => m.FolderPageModule)
  },
  {
    path: 'compute',
    loadChildren: () => import('./compute/compute.module').then( m => m.ComputePageModule)
  },
  {
    path: 'datasets',
    loadChildren: () => import('./datasets/datasets.module').then( m => m.DatasetsPageModule)
  },
  {
    path: 'workflows',
    loadChildren: () => import('./workflows/workflows.module').then( m => m.WorkflowsPageModule)
  },
  {
    path: 'cardinals',
    loadChildren: () => import('./cardinals/cardinals.module').then( m => m.CardinalsPageModule)
  },
  {
    path: 'analytics',
    loadChildren: () => import('./analytics/analytics.module').then( m => m.AnalyticsPageModule)
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
