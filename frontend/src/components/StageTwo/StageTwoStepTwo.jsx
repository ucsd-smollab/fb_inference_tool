import { Link } from "react-router-dom";

import StepTwoProfileSection from "./StepTwoProfileSection";
import StepTwoKnowsSection from "./StepTwoKnowsSection";
import StepTwoShowsSection from "./StepTwoShowsSection";


import styles from "./StageTwoStepTwo.module.css";
import globalStyles from "./StageTwo.module.css";

const StageTwoStepTwo = (props) => {
  return (
    <div className={globalStyles.background}>
      <br />
      <div className={styles.MainBodyContainer}>
        <StepTwoProfileSection />
        <StepTwoKnowsSection />
        <StepTwoShowsSection />
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/">
          <button className={globalStyles.ButtonNav}>
            Next
          </button>
        </Link>
      </div>
    </div>
  );
}
  
export default StageTwoStepTwo;