import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import mainStyles from "./StageThree.module.css";

const StageThreeStepTwoTwo = (props) => {
  const [friendsExplicit, changeFriendsExplicit] = useState([]);
  const [friendsInferred, changeFriendsInferred] = useState([]);
  const [prediction, changePrediction] = useState([]);

  useEffect(() => {
    changeFriendsExplicit([
      "Andy Nafets",
      "Aaron B",
      "Stephen T",
      "Mary A",
      "Kristen V",
    ]);
    changeFriendsInferred([
      "Andy Nafets",
      "Aaron B",
      "Stephen T",
      "Mary A",
      "Kristen V",
    ]);
    changePrediction("have lived in San Diego");
  }, []);

  return (
    <div className={globalStyles.background}>
      <br />
      <div>
        <div className={globalStyles.StageTitleContainer}>
          <h1>
            We can infer that these friends also {prediction}
          </h1>
        </div >
        <br />
        <br />
        <div className={globalStyles.mainContent}>
        <div className={`${globalStyles.flex_container} ${globalStyles.two_column}`}>
          <div className={`${globalStyles.itemBoxes} ${globalStyles.longBox} ${globalStyles.wideBox}`}>
            <h2>Friends who explicitly shared that they {prediction}</h2>
            {friendsExplicit.map((friend) => (
              <div className={globalStyles.medText}>
                <span>{friend}</span>
              </div>
            ))}
          </div>
        </div>
        <div className={`${globalStyles.flex_container} ${globalStyles.two_column}`}>
          <div className={`${globalStyles.itemBoxes} ${globalStyles.longBox} ${globalStyles.wideBox}`}>
            <h2>Friends who we can infer {prediction}</h2>
            {friendsInferred.map((friend) => (
              <div className={globalStyles.medText}>
                <span>
                {friend}
                </span>
              </div>
            ))}
          </div>
        </div>
        </div>
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageThreeStepThree">
          <button className={globalStyles.ButtonNav}>Next</button>
        </Link>
      </div>
    </div>
  );
};

export default StageThreeStepTwoTwo;
