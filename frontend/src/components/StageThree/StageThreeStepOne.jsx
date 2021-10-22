import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import globalStyles from "./StageThree.module.css";

const StageThreeStepOne = (props) => {
  const [friendsManyShared, changeFriendsMany] = useState([]);
  const [friendsSparseShared, changeFriendsSparse] = useState([]);

  useEffect(() => {
    // make call to fetch friends
    changeFriendsMany(["a", "b", "c", "d", "e"]);
    changeFriendsSparse(["z", "y", "x", "w", "v"]);
  }, []);

  return (
    <div className={globalStyles.background}>
      <br />
      <div className={globalStyles.MainBodyContainer}>
        <div className={globalStyles.CenterTitleContainer}>
          <span className={globalStyles.CenterTitle}>Your Friends</span>
        </div>
        <div className={globalStyles.ContentContainer}>
          <div>
            <span className={globalStyles.StageTitle}>
              Some of your friends have shared a lot:
            </span>
            <br />
            <br />
            <div className={globalStyles.FriendsContainer}>
              {friendsManyShared.map((friend) => (
                <div className={globalStyles.FriendItem}>
                  <span>{friend}</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <span>Others haven't shared much at all:</span>
            <br />
            <br />
            <div className={globalStyles.FriendsContainer}>
              {friendsSparseShared.map((friend) => (
                <div className={globalStyles.FriendItem}>
                  <span>{friend}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageThreeStepTwoOne">
          <button className={globalStyles.ButtonNav}>Next</button>
        </Link>
      </div>
    </div>
  );
};

export default StageThreeStepOne;
