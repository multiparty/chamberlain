import { Component, OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-compute',
  templateUrl: './compute.page.html',
  styleUrls: ['./compute.page.scss'],
})
export class ComputePage implements OnInit {

  private currentDataset = '';
  private datasets = [];
  private operations = {'':[]};

  constructor(
    private http: HttpService
  ) { }

  async ngOnInit() {
    const datasetResponse = await this.http.getAllDatasets().toPromise();
    if (!datasetResponse.error) {
      this.datasets = [...new Set(datasetResponse.datasets.map(ds => ds[2]))];
      this.currentDataset = this.datasets[0];
      for (const ds of this.datasets) {
        this.operations[ds] = [];
      }
    }
    const workflowResponse = await this.http.getAllWorkflows().toPromise();
    console.log(workflowResponse);
    if (!workflowResponse.error) {
      const workflows = workflowResponse.workflows;

      const workflowRelResponse = await this.http.getWorkflowRelationships().toPromise();
      console.log(workflowRelResponse);
      if (!workflowRelResponse.error) {
        const rels = workflowRelResponse.workflow_relationships;
        for (const rel of rels) {
          this.operations[rel[1]].push(workflows.filter(ws => ws[1] === rel[2])[0][2]);
        }
      }
    }

    console.log(this.datasets);
    console.log(this.operations);
  }

}
