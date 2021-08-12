import { Component } from '@angular/core';
@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
})
export class AppComponent {
  public appPages = [
    { title: 'Datasets', url: '/datasets', icon: 'analytics' },
    { title: 'Workflows', url: '/workflows', icon: 'reader' },
    { title: 'Cardinals', url: '/cardinals', icon: 'cloud' },
    { title: 'Compute', url: '/compute', icon: 'calculator' },
  ];
  constructor() {}
}
