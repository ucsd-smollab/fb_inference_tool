import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import styles from "./StageThree.module.css";

const StageThreeStepTwoTwo = (props) => {
  const [friendsExplicit, changeFriendsExplicit] = useState([]);
  const [friendsInferred, changeFriendsInferred] = useState([]);
  const [prediction, changePrediction] = useState([]);

  useEffect(() => {
    const responseUsersShared= fetch("http://localhost:5000/stage_three_step_two", {
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
      <h1>{prediction}</h1>
      <div className={styles.flex_container}>
        <span className={styles.flex_items}>
          <h3>Shared:</h3>
          {friendsExplicit.map((friend) => (
            <div className={globalStyles.medText}>
              <div>{friend}</div>
            </div>
          ))}
        </span>
        <span className={styles.flex_items}>
            <h3>Inferred:</h3>
            {friendsInferred.map((friend) => (
              <div className={globalStyles.medText}>
                <div>{friend}</div>
              </div>
            ))}
        </span>
      </div>
    <div className={globalStyles.ButtonContainer}>
      <Link to="/StageThreeStepThree">
        <button className={globalStyles.ButtonNav} >Next</button>
      </Link>
    </div>
    </div>
  );
};

export default StageThreeStepTwoTwo;
