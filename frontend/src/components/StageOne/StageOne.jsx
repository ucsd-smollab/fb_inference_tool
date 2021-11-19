import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import styles from "./StageOne.module.css";

const StageOne = (props) => {
  return (
    <div className={globalStyles.background}>
      <h1>What have you shared on your profile?</h1>
      <div class={globalStyles.mainContent} >
      <div class={styles.centered}>
      <a href="https://www.facebook.com/profile" target="_blank" rel="noopener noreferrer">
      <button class={styles.linktofb}>
        View Your Info
      </button>
      </a>
      </div>
        <div className={globalStyles.ButtonContainer}>
          <Link to="/StageTwoStepOne">
            <button className={globalStyles.ButtonNav}>
              Next
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default StageOne;
