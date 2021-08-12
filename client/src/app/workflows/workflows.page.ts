import { Component, OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-workflows',
  templateUrl: './workflows.page.html',
  styleUrls: ['./workflows.page.scss'],
})
export class WorkflowsPage implements OnInit {

  private rows: any;

  private columns = [
    { name: 'Workflow ID', prop: 'workflowId'},
    { name: 'Operation', prop: 'operationName'},
    { name: 'Dataset ID', prop: 'datasetId'},
  ];

  constructor(
    private http: HttpService
  ) { }

  async ngOnInit() {

    let workflows;

    const workflowResponse = await this.http.getAllWorkflows().toPromise();
    if (!workflowResponse.error) {
      workflows = workflowResponse.workflows;
    }

    this.rows = this.formatTableData(workflows);
    console.log(this.rows);
  }


  formatTableData(workflows) {
    // Workflow ID | Operation | Dataset Id
    console.log(workflows);
    const objects = [];

    for (const workflow of workflows) {
      objects.push(
        {
          workflowId: workflow[1],
          operationName: workflow[2],
          datasetId: workflow[3]
          
        }
      );
    }
    return objects;
  }

}