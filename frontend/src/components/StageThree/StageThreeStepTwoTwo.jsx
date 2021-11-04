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
    changePrediction("lived in San Diego");
  }, []);

  return (
    <div className={globalStyles.background}>
      <br />
      <div className={mainStyles.CenterTitleContainer}>
        <span className={mainStyles.CenterTitle}>
          {`We can infer that these friends have also ${prediction}`}
        </span>
      </div>
      <div className={mainStyles.MainBodyContainer}>
        <div className={mainStyles.ContentContainer}>
          <div>
            <span className={mainStyles.StageTitle}>
              {`Friends who explicitly shared that they ${prediction}`}
            </span>
            <br />
            <div className={mainStyles.FriendsContainer}>
              {friendsExplicit.map((friend) => (
                <div className={mainStyles.FriendItem}>
                  <span>{friend}</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <span
              className={mainStyles.StageTitle}
            >{`Friends who we can infer ${prediction}`}</span>
            <br />
            <div className={mainStyles.FriendsContainer}>
              {friendsInferred.map((friend) => (
                <div className={mainStyles.FriendItem}>
                  <span>{friend}</span>
                  <div className={mainStyles.FriendItemHoverText}>
                    <span
                      style={{ fontSize: "35px" }}
                    >{`You and ${friend} have mutual friends, 5 of whom have prediction`}</span>
                  </div>
                </div>
              ))}
              <br />
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
