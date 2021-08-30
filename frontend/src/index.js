import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import reportWebVitals from "./reportWebVitals";

import "./index.css";
import App from "./App";
import {StageTwoStepOne, StageTwoStepTwo} from "./components";

ReactDOM.render(
  <Router>
    <Switch>
		  <Route exact path="/" component={App}/>
			<Route exact path="/StageTwoStepOne" component={StageTwoStepOne} />
      <Route exact path="/StageTwoStepTwo" component={StageTwoStepTwo} />
	  </Switch>
  </Router>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
