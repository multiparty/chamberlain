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
    { name: 'Total Run time', prop: 'runTime'}
  ];

  private aggRows: any;
  private aggColumns = [
    { name: 'Statistic', prop: 'stat'},
    { name: 'CPU Usage', prop: 'cpuVal'},
    { name: 'Memory Usage', prop: 'memVal'},
    { name: 'Total Run time', prop: 'timeVal'},
  ];

  constructor(
    private http: HttpService
  ) { }

  async ngOnInit() {
    const runningJobsResponse = await this.http.getAllRunningJobs().toPromise();
    if (!runningJobsResponse.error) {
      console.log(runningJobsResponse);
      this.runningJobs = runningJobsResponse.running_jobs;
      this.rows = this.formatTableData();
      this.aggRows = this.formatAggregateTable();
    }
  }

  formatTableData() {
    const objects = [];
    for (const job of this.runningJobs) {
      objects.push({
        workflowName: job[1],
        cpuUsage: job[5],
        memoryUsage: job[6],
        runTime: job[8]
      })
    }
    return objects;
  }


  formatAggregateTable() {
    const allCpu = this.rows.filter(obj => obj.cpuUsage !== null).map(obj => obj.cpuUsage);
    const allMem = this.rows.filter(obj => obj.memoryUsage !== null).map(obj => obj.memoryUsage);
    const allTime = this.rows.filter(obj => obj.runTime !== null).map(obj => obj.runTime);
    const reducer = (accumulator, currentValue) => accumulator + currentValue;

    const sumCpu = allCpu.reduce(reducer);
    const sumMem = allMem.reduce(reducer);
    const sumTime = allTime.reduce(reducer);

    const avgCpu = (sumCpu/allCpu.length).toFixed(4);
    const avgMem = (sumMem/allMem.length).toFixed(4);
    const avgTime = (sumTime/allTime.length).toFixed(4);
    const objects = [];
    objects.push({
      stat: 'Maximum',
      cpuVal: Math.max(...allCpu),
      memVal: Math.max(...allMem),
      timeVal: Math.max(...allTime),
    });
    objects.push({
      stat: 'Minimum',
      cpuVal: Math.min(...allCpu),
      memVal: Math.min(...allMem),
      timeVal: Math.min(...allTime)
    });
    objects.push({
      stat: 'Average',
      cpuVal: avgCpu,
      memVal: avgMem,
      timeVal: avgTime
    });
    objects.push({
      stat: 'Sum',
      cpuVal: sumCpu,
      memVal: sumMem,
      timeVal: sumTime
    });
    return objects;

  }

}
