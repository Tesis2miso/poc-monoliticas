import http from 'k6/http';
import { SharedArray } from 'k6/data';
import { check } from 'k6';
import { URL } from 'https://jslib.k6.io/url/1.0.0/index.js';

export const options = {
  insecureSkipTLSVerify: true,
  noConnectionReuse: false,
  scenarios: {
    create_product: {
      executor: 'ramping-vus',
      exec: 'create_product',
      startVUs: 1,
      stages: [
        { duration: '10s', target: 1 },
      ]
    },
    list_products: {
      executor: 'ramping-vus',
      exec: 'list_products',
      startVUs: 1,
      stages: [
        { duration: '10s', target: 1 },
      ]
    },
  },
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)', 'count'],
  thresholds: {}
};

for (let key in options.scenarios) {
  let thresholdName = `http_req_duration{scenario:${key}}`;
  if (!options.thresholds[thresholdName]) {
    options.thresholds[thresholdName] = [];
  }
}

for (let key in options.scenarios) {
  let thresholdName = `http_req_failed{scenario:${key}}`;
  if (!options.thresholds[thresholdName]) {
    options.thresholds[thresholdName] = [];
  }
}

export function create_product() {
  let headers = {
    'Content-Type': 'application/json',
  }
  //let randomServiceIndex = Math.floor(Math.random() * services.length);
  var body = {
    nombre: "Test",
    stock: 100 + Math.floor(Math.random() * 100)
  };

  let res = http.post(
    `http://34.70.186.96:3001/productos`,
    JSON.stringify(body),
    { headers: headers }
  );

  check(res, {
    'Status is 203': (r) => r.status === 203
  });
}

export function list_products() {
  //let randomIndex = Math.floor(Math.random() * data.length);
  let headers = {};
  let res = http.get(
    `http://34.70.186.96:3001/productos`,
    { headers: headers }
  );

  check(res, {
    'Status is 200': (r) => r.status === 200
  });
}