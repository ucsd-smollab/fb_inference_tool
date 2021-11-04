import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import CategorySelection from "./components/categorySelection";
import ColumnData from "./components/ColumnData";

import globalStyles from "./StageThree.module.css";
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
      <br />
      <br />
      <br />
      <br />
      <div className={globalStyles.CenterTitleContainer}>
        <span className={globalStyles.CenterTitle}>Select a Category</span>
      </div>
      <br />
      <br />
      <br />
      <br />
      <div className={globalStyles.MainBodyContainer}>
        <div className={styles.CategoryListContainer}>
          {categories.map((category) => (
            <CategorySelection
              category={category}
              changeCategory={selectCateory}
              selectedCategory={categorySelected}
            />
          ))}
        </div>

        <div className={styles.DataContainer}>
          <div className={styles.ColumnContainer}>
            <span>shared directly</span>
            <ColumnData data={friendsDirect} />
          </div>
          <div className={styles.ColumnContainer}>
            <span>inferred</span>
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
