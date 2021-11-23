import globalStyles from "../../../styles/styles.module.css";

const FriendBox = (props) => {
  return (
    <div className={globalStyles.wrapper}>
      <div className={globalStyles.friendInfoHeader}>
        <div className={globalStyles.headerContainer}>
          <span> 
            <img className={globalStyles.profilePicture} src={props.friend.profilePictureURL}/> 
          </span>
          <span>
            <div className={globalStyles.friendName}>{props.friend.name}</div>
            <div className={globalStyles.friendH4}>{props.friend.mutualFriendCount} Mutual Friends</div>
          </span>
        </div>
      </div>

      <div className={globalStyles.friendInfo}>
        <div className={globalStyles.headerContainer} style={{"marginLeft": "20px"}}>
          <div className={globalStyles.about}>About</div>
        </div>

        <div className={globalStyles.centerColumn}>
          <div className={globalStyles.centerColumnInfo}>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>Workplace</div>
                {props.friend.workplace.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
            </div>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>College</div>
                {props.friend.college.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
            </div>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>High School</div>
                {props.friend.highschool.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
            </div>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>Places Lived</div>
                {props.friend.places.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
            </div>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>Religious Views</div>
                {props.friend.religion.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
            </div>
            <div className={globalStyles.categoryName}>Political Views</div>
              {props.friend.politics.map( (entry) =>
                  <div className={globalStyles.knownInfo}>{entry}</div>
              )}
            </div>
        </div>
      </div>
    </div>
  );
};

export default FriendBox;
