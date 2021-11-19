import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import mainStyles from "./StageThree.module.css";

const StageThreeStepTwoOne = (props) => {
  const [friendsExplicit, changeFriendsExplicit] = useState([]);
  const [friendsInferred, changeFriendsInferred] = useState([]);
  const [prediction, changePrediction] = useState([]);

  useEffect(() => {
    const responseUsersShared= fetch("http://localhost:5000/stage_three_step_two_one_one", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    }).then(res => res.json()).then(data => {
      changePrediction(data[0])
      changeFriendsExplicit(data[1])
      changeFriendsInferred(data[2])
    });
  }, []);

  return (
    <div className={globalStyles.background}>
      <br />
      <div>
        <div className={globalStyles.StageTitleContainer}>
          <h1>
            {prediction}
          </h1>
        </div >
        <br />
        <br />
        <div className={globalStyles.mainContent}>
        <div className={`${globalStyles.flex_container} ${globalStyles.two_column}`}>
          <div className={`${globalStyles.itemBoxes} ${globalStyles.longBox} ${globalStyles.wideBox}`}>
            {friendsExplicit.map((friend) => (
              <div className={globalStyles.medText}>
                <span>{friend}</span>
              </div>
            ))}
          </div>
        </div>
        <div className={`${globalStyles.flex_container} ${globalStyles.two_column}`}>
          </div>
        </div>
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageThreeStepTwoTwo">
          <button className={globalStyles.ButtonNav}>Next</button>
        </Link>
      </div>
    </div>
  );
};

export default StageThreeStepTwoOne;
