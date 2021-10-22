import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import StageOne from "./components/StageOne/StageOne";
import StageTwoStepOne from "./components/StageTwo/StageTwoStepOne";
import StageTwoStepTwo from "./components/StageTwo/StageTwoStepTwo";
import StageThreeStepOne from "./components/StageThree/StageThreeStepOne";
import StageThreeStepTwoOne from "./components/StageThree/StageThreeStepTwoOne";
import StageThreeStepTwoTwo from "./components/StageThree/StageThreeStepTwoTwo";
import StageThreeStepThree from "./components/StageThree/StageThreeStepThree";


const App = (props) => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={StageOne}/>
        <Route exact path="/StageTwoStepOne" component={StageTwoStepOne} />
        <Route exact path="/StageTwoStepTwo" component={StageTwoStepTwo} />
        <Route exact path="/StageThreeStepOne" component={StageThreeStepOne} />
        <Route exact path="/StageThreeStepTwoOne" component={StageThreeStepTwoOne} />
        <Route exact path="/StageThreeStepTwoTwo" component={StageThreeStepTwoTwo} />
        <Route exact path="/StageThreeStepThree" component={StageThreeStepThree} />
      </Switch>
    </Router>
  );
}

export default App;
