let persons = [
    {
      id: 1,
      name: "Jan Kowalski"
    }, {
      id: 2,
      name: "John Doe"
    }, {
      id: 3,
      name: "Jarek Kaczka"
    }
  ];
  
  let ages = [
    {
      person: 1,
      age: 18
    }, {
      person: 2,
      age: 24
    }, {
      person: 3,
      age: 666
    }
  ];
  
  let locations = [
    {
      person: 1,
      country: "Poland"
    }, {
      person: 3,
      country: "Poland"
    }, {
      person: 1,
      country: "USA"
    }
  ];
  
  let averageAge = ages
  .filter(age => locations.some(location => location.person === age.person && location.country === 'Poland'))
  .map(age => age.age)
  .reduce((acc, age, index, arr) => acc + age / arr.length, 0);

  console.log('Average age:', averageAge);

  