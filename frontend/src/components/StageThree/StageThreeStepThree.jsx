import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import CategorySelection from "./components/categorySelection";
import ColumnData from "./components/ColumnData";

import globalStyles from "../../styles/styles.module.css";
import mainStyles from "./StageThree.module.css";
import styles from "./StageThreeStepThree.module.css";

const StageThreeStepThree = (props) => {
  const [categories, changeCategories] = useState([]);
  const [categorySelected, changeCategorySelected] = useState("");

  const [friendsDirect, changeFriendsDirect] = useState([]);
  const [friendsInferred, changeFriendsInferred] = useState([]);

  const [friendsDirectMap, changeFriendsDirectMap] = useState({});
  const [friendsInferredMap, changeFriendsInferredMap] = useState({});

  useEffect(() => {
    // make call to fetch friends
    let friendsDirectCategories = [["shared SD"], ["shared Arby's"], ["shared Camden High"], ["shared Catholic"]];
    let friendsInferredCategories = [["inferred SD"], ["inferred Arby's"], ["inferred Camden High"], ["inferred Catholic"]];
    let fetchedCategories =  [
      "friends who have lived in San Diego",
      "friends who have worked at Arby's",
      "friends who attended Camden High",
      "friends who are Catholic",
    ]

    let friendsDMap = {};
    let friendsIMap = {};

    changeCategories(fetchedCategories);

    for (let i = 0; i < fetchedCategories.length; i++) {
      friendsDMap[fetchedCategories[i]] = friendsDirectCategories[i];
      friendsIMap[fetchedCategories[i]] = friendsInferredCategories[i];
    }

    // updated state
    changeFriendsDirectMap(friendsDMap);
    changeFriendsInferredMap(friendsIMap);
  }, []);

  const selectCateory = (category) => {
    changeCategorySelected(category);
    changeFriendsDirect(friendsDirectMap[category]);
    changeFriendsInferred(friendsInferredMap[category]);
  };

  return (
    <div className={globalStyles.background}>
      <div>
        <h1>Select a Category</h1>
      </div>
      <div className={globalStyles.mainContent}>
        <div>
          {categories.map((category) => (
            <CategorySelection
              category={category}
              changeCategory={selectCateory}
              selectedCategory={categorySelected}
            />
          ))}
        </div>
      </div>

      <div className={globalStyles.mainContent}>
      <div className={`${globalStyles.flex_container} ${globalStyles.two_column}`}>
        <div className={`${globalStyles.itemBoxes} ${globalStyles.longBox}`}>
            <div><h2>Shared directly</h2></div>
            <ColumnData data={friendsDirect} />
        </div>
        <div className={`${globalStyles.itemBoxes} ${globalStyles.longBox}`}>
            <div><h2>Inferred</h2></div>
            <ColumnData data={friendsInferred} />
        </div>
      </div>
      </div>
      <div className={globalStyles.ButtonContainer}>
        <Link to="/StageFour">
          <button className={globalStyles.ButtonNav}>Next</button>
        </Link>
      </div>
    </div>
  );
};

export default StageThreeStepThree;
