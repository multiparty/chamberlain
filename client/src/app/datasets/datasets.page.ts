import { Component, OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-datasets',
  templateUrl: './datasets.page.html',
  styleUrls: ['./datasets.page.scss'],
})
export class DatasetsPage implements OnInit {

  private rows: any;

  private columns = [
    { name: 'Dataset ID', prop: 'datasetId'},
    { name: 'Schema', prop: 'schema'},
    { name: 'Compatible Workflows', prop: 'workflows'},
    { name: 'Locations', prop: 'locations'}
  ];

  constructor(
    private http: HttpService
  ) { }

  async ngOnInit() {

    let datasets;
    let storageRels;
    let workflowRels;

    const datasetResponse = await this.http.getAllDatasets().toPromise();
    if (!datasetResponse.error) {
      datasets = datasetResponse.datasets;
    }
    const storageRelResponse = await this.http.getStorageRelationships().toPromise();
    if (!storageRelResponse.error) {
      storageRels = storageRelResponse.storage_relationships;
    }
    const workflowRelResponse = await this.http.getWorkflowRelationships().toPromise();
    if (!workflowRelResponse.error) {
      workflowRels = workflowRelResponse.workflow_relationships;
    }

    this.rows = this.formatTableData(datasets, storageRels, workflowRels);
    console.log(this.rows);
  }


  formatTableData(datasets, storageRels, workflowRels) {
    // Dataset ID | Schema | Compatible Workflows | Locations
    console.log(datasets);
    console.log(storageRels);
    console.log(workflowRels);
    const uniqueIds = [...new Set(datasets.map(ds => ds[2]))];
    const objects = [];

    for (const id of uniqueIds) {
      objects.push(
        {
          datasetId: id,
          schema: datasets.filter(ds => ds[2] === id)[0][3],
          workflows: workflowRels.filter(wk => wk[1] === id).map(wk => wk[2]).join(),
          locations: storageRels.filter(st => st[1] === id)[0][2]
        }
      );
    }
    return objects;
  }



}
