import { Component, OnInit } from '@angular/core';
import { HttpService } from "../services/http.service";

@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.page.html',
  styleUrls: ['./analytics.page.scss'],
})
export class AnalyticsPage implements OnInit {

  private runningJobs;

  // data table variables
  private rows: any;
  private columns = [
    { name: 'Computation ID', prop: 'workflowName'},
    { name: 'CPU Usage', prop: 'cpuUsage'},
    { name: 'Memory Usage', prop: 'memoryUsage'},
    // { name: 'Profiling Timestamps', prop: 'profiling'}
  ];

  constructor(
    private http: HttpService
  ) { }

  async ngOnInit() {
    const runningJobsResponse = await this.http.getAllRunningJobs().toPromise();
    // let jobs;
    if (!runningJobsResponse.error) {
      console.log(runningJobsResponse);
      this.runningJobs = runningJobsResponse.running_jobs;
      this.rows = this.formatTableData();
    }
  }

  formatTableData() {
    const objects = [];
    for (const job of this.runningJobs) {
      objects.push(
        {
          workflowName: job[1],
          cpuUsage: job[5],
          memoryUsage: job[6],
        }
      )
    }
    return objects;
  }

}
