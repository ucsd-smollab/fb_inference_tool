import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import StageOne from "./components/StageOne";
import StageTwoStepOne from "./components/StageTwoStepOne";
import StageTwoStepTwo from "./components/StageTwoStepTwo";

const App = (props) => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={StageOne}/>
        <Route exact path="/StageTwoStepOne" component={StageTwoStepOne} />
        <Route exact path="/StageTwoStepTwo" component={StageTwoStepTwo} />
      </Switch>
    </Router>
  );
}

export default App;
