import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import StageOne from "./components/StageOne/StageOne";
import StageTwoStepOne from "./components/StageTwo/StageTwoStepOne";
import StageTwoStepTwo from "./components/StageTwo/StageTwoStepTwo";
import StageThreeStepOne from "./components/StageThree/StageThreeStepOne";

const App = (props) => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={StageOne}/>
        <Route exact path="/StageTwoStepOne" component={StageTwoStepOne} />
        <Route exact path="/StageTwoStepTwo" component={StageTwoStepTwo} />
        <Route exact path="/StageThreeStepOne" component={StageThreeStepOne} />
      </Switch>
    </Router>
  );
}

export default App;
