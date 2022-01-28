import { Link } from "react-router-dom";

import StepTwoProfileSection from "./StepTwoProfileSection";
import StepTwoKnowsSection from "./StepTwoKnowsSection";
import StepTwoShowsSection from "./StepTwoShowsSection";

import globalStyles from "../../styles/styles.module.css";
import styles from "./StageTwoStepTwo.module.css";

const StageTwoStepTwo = (props) => {
  const stopScraper = () => {
    const stop_scrapper_request = fetch("http://127.0.0.1:5000/stop_scraper", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    })
  };

  return (
    <div className={globalStyles.background}>
      <div className={globalStyles.mainContent}>
        <StepTwoProfileSection />
        <StepTwoKnowsSection />
        <StepTwoShowsSection />
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageThreeStepOne">
          <button className={globalStyles.ButtonNav} onClick={() => {
            stopScraper();
            console.log("called stopScraper");
          }}>Next</button>
        </Link>
      </div>
    </div>
  );
}

export default StageTwoStepTwo;
