import { Link } from "react-router-dom";

import StepTwoProfileSection from "./StepTwoProfileSection";
import StepTwoKnowsSection from "./StepTwoKnowsSection";
import StepTwoShowsSection from "./StepTwoShowsSection";

import globalStyles from "../../styles/styles.module.css";
import styles from "./StageTwoStepTwo.module.css";

const StageTwoStepTwo = (props) => {
  return (
    <div className={globalStyles.background}>
      <div className={globalStyles.mainContent}>
        <StepTwoProfileSection />
        <StepTwoKnowsSection />
        <StepTwoShowsSection />
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageThreeStepOne">
          <button className={globalStyles.ButtonNav}>
            Next
          </button>
        </Link>
      </div>
    </div>
  );
}
  
export default StageTwoStepTwo;