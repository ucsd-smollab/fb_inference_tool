import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import globalStyles from "./StageThree.module.css";

const StageThreeStepOne = (props) => {
  const [friendsManyShared, changeFriendsMany] = useState([]);
  const [friendsSparseShared, changeFriendsSparse] = useState([]);

  useEffect(() => {
    // make call to fetch friends
    changeFriendsMany(["wow"]);
    changeFriendsSparse(["sparse"]);
  }, [])

  return (
    <div className={globalStyles.background}>
      <br />
      <div className={globalStyles.MainBodyContainer}>
        <span className={globalStyles.CenterTitle}>
          Your Friends
        </span>
        <div className={globalStyles.ContentContainer}>
          <div>
            <span>Some of your friends have shared a lot:</span>
            {friendsManyShared.map((friend) => 
              <span>{friend}</span>
            )}
          </div>
          <div>
            <span>Others haven't shared much at all:</span>
            {friendsSparseShared.map((friend) => 
              <span>{friend}</span>
            )}
          </div>
        </div>
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageTwoStepTwo">
          <button className={globalStyles.ButtonNav}>Next</button>
        </Link>
      </div>
    </div>
  );
};

export default StageThreeStepOne;
