import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import globalStyles from "../../styles/styles.module.css";
import mainStyles from "./StageThree.module.css";

const StageThreeStepTwoOne = (props) => {
  const [friends, changeFriends] = useState([]);

  useEffect(() => {
    changeFriends([
      "Andy Nafets",
      "Aaron B",
      "Stephen T",
      "Mary A",
      "Kristen V",
    ]);
  }, []);

  return (
    <div className={globalStyles.background}>
      <br />
      <div className={mainStyles.MainBodyContainer}>
        <div className={mainStyles.CenterTitleContainer}>
          <span className={mainStyles.CenterTitle}>
            Some of your friends who have lived in San Diego:
          </span>
        </div>
        <br />
        <br />
        <div className={mainStyles.ContentContainer}>
          <div className={mainStyles.FriendsContainer}>
            {friends.map((friend) => (
              <div className={mainStyles.FriendItem}>
                <span>{friend}</span>
              </div>
            ))}
          </div>
          <div>
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
