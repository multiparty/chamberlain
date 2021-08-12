import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Platform } from '@ionic/angular';
import { environment } from '../../environments/environment';
import { forkJoin, Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  private serverUrl;

  constructor(
    private http: HttpClient,
    private platform: Platform,
  ) {
    this.serverUrl = environment.serverUrl;
  }

  /* * * * * * */
  /* DATASETS  */
  /* * * * * * */

  getAllDatasets() {
    return this.http.get(this.serverUrl + '/api/dataset').pipe(
      catchError(val => of(val)),
    );
  }

  getOneDataset(id) {
    return this.http.get(this.serverUrl + `/api/dataset/${id}`).pipe(
      catchError(val => of(val)),
    );
  }

  /* * * * * * */
  /* WORKFLOWS */
  /* * * * * * */

  getAllWorkflows() {
    return this.http.get(this.serverUrl + '/api/workflow').pipe(
      catchError(val => of(val)),
    );
  }

  getOneWorkflow(id) {
    return this.http.get(this.serverUrl + `/api/workflow/${id}`).pipe(
      catchError(val => of(val)),
    );
  }

  /* * * * * * * * */
  /* RELATIONSHIPS */
  /* * * * * * * * */

  getStorageRelationships() {
    return this.http.get(this.serverUrl + `/api/storage-relationship`).pipe(
      catchError(val => of(val)),
    );
  }

  getWorkflowRelationships() {
    return this.http.get(this.serverUrl + `/api/workflow-relationship`).pipe(
      catchError(val => of(val)),
    );
  }

  /* * * * * * */
  /* CARDINALS  */
  /* * * * * * */

  getAllCardinals() {
    return this.http.get(this.serverUrl + '/api/cardinal').pipe(
      catchError(val => of(val)),
    );
  }

  getOneCardinal(id) {
    return this.http.get(this.serverUrl + `/api/cardinal/${id}`).pipe(
      catchError(val => of(val)),
    );
  }

  /* * * * * */
  /* COMPUTE */
  /* * * * * */

  submitComputation(submit_request) {
    return this.http.post(this.serverUrl + `/api/submit`, submit_request).pipe(

      catchError(val => of(val)),
    );
  }

}























