import globalStyles from "../../../styles/styles.module.css";

const FriendBox = (props) => {
  return (
    <div style={{"marginTop":"90px"}} className={globalStyles.wrapper}>
      {props.friend.initialized && (<div className={globalStyles.friendInfoHeader}>
        <div className={globalStyles.headerContainer}>
          <span>
            <img className={globalStyles.profilePicture} src={props.friend.shared.profilePictureURL}/>
          </span>
          <span>
            <div className={globalStyles.friendName}>{props.friend.shared.name}</div>
            <div className={globalStyles.friendH4}>{props.friend.shared.mutualFriendCount} Mutual Friends</div>
          </span>
        </div>
      </div>)}

      {props.friend.initialized && (<div className={globalStyles.friendInfo}>
        <div className={globalStyles.headerContainer} style={{"marginLeft": "20px"}}>
          <div className={globalStyles.about}>About</div>
        </div>

        <div className={globalStyles.centerColumn}>
          <div className={globalStyles.centerColumnInfo}>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>Workplace</div>
                {props.friend.shared.workplace.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
                {props.friend.inferred.work && <div className={globalStyles.inferredInfo}>{props.friend.inferred.work} (inferred)</div>}
            </div>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>College</div>
                {props.friend.shared.college.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
                {props.friend.inferred.college && <div className={globalStyles.inferredInfo}>{props.friend.inferred.college} (inferred)</div>}
            </div>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>High School</div>
                {props.friend.shared.highschool.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
                {props.friend.inferred.highschool && <div className={globalStyles.inferredInfo}>{props.friend.inferred.highschool} (inferred)</div>}
            </div>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>Places Lived</div>
                {props.friend.shared.places.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
                {props.friend.inferred.places && <div className={globalStyles.inferredInfo}>{props.friend.inferred.places} (inferred)</div>}
            </div>
            <div className={globalStyles.centerColumnItem}>
              <div className={globalStyles.categoryName}>Religious Views</div>
                {props.friend.shared.religion.map( (entry) =>
                    <div className={globalStyles.knownInfo}>{entry}</div>
                )}
                {props.friend.inferred.religion && <div className={globalStyles.inferredInfo}>{props.friend.inferred.religion} (inferred)</div>}
            </div>
            <div className={globalStyles.categoryName}>Political Views</div>
              {props.friend.shared.politics.map( (entry) =>
                  <div className={globalStyles.knownInfo}>{entry}</div>
              )}
              {props.friend.inferred.political && <div className={globalStyles.inferredInfo}>{props.friend.inferred.political} (inferred)</div>}
            </div>
        </div>
      </div>)}
    </div>
  );
};

export default FriendBox;
