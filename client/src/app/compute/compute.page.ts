import { Component, OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-compute',
  templateUrl: './compute.page.html',
  styleUrls: ['./compute.page.scss'],
})
export class ComputePage implements OnInit {

  private errorMsg = '';
  private successMsg = '';
  private isWaiting = false;
  private currentDataset = '';
  private currentOp = '';
  private numParties = 3;
  private datasets = [];
  private operations = {'':[]};

  constructor(
    private http: HttpService
  ) { }

  async ngOnInit() {
    const datasetResponse = await this.http.getAllDatasets().toPromise();
    if (!datasetResponse.error) {
      this.datasets = [...new Set(datasetResponse.datasets.map(ds => ds[1]))];
      this.currentDataset = this.datasets[0];
      for (const ds of this.datasets) {
        this.operations[ds] = [];
      }
    }
    const workflowResponse = await this.http.getAllWorkflows().toPromise();
    if (!workflowResponse.error) {
      const workflows = workflowResponse.workflows;

      const workflowRelResponse = await this.http.getWorkflowRelationships().toPromise();
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

  validateParameters() {
    if (this.currentDataset === '') {
      this.errorMsg = 'Please select a dataset';
      return false;
    }
    if (this.currentOp === '') {
      this.errorMsg = 'Please select an operation';
      return false;
    }
    if (this.numParties < 3) {
      this.errorMsg = 'The number of parties must be at least 3';
      return false;
    }
    return true;
  }

  findDestination(response) {
    for (const msg of response) {
      if ('DESTINATION' in msg) {
        return msg['DESTINATION'];
      }
    }
  }

  async submitComputation() {
    console.log('here');
    this.errorMsg = '';
    this.successMsg = '';
    const valid = this.validateParameters();

    if (valid) {
      this.isWaiting = true;
      this.successMsg = 'Your workflow has been submitted! Please wait here to see where your result will be located. (This may take up to a few minutes)';
      const req = {
        party_count: this.numParties,
        party_list: [...Array(this.numParties+1).keys()].slice(1),
        dataset_id: this.currentDataset,
        operation: this.currentOp
      };

      console.log(req);

      const submitResponse = await this.http.submitComputation(req).toPromise();
      console.log(submitResponse);
      this.isWaiting = false;
      if ('ERR' in submitResponse) {
        this.errorMsg = submitResponse['ERR'];
        this.successMsg = '';
      } else {
        this.successMsg = `Your result will be located at this S3 Bucket: ${this.findDestination(submitResponse['MSG'])}. Please wait for a few minutes before checking.`;
      }
    }
  }

}
