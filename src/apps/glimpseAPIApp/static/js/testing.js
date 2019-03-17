var allSections = []
var allDevices = []
var allDeviceSections = {}
var currentDevice;
var deviceSectionIndex = 0;
function getAllSections(){
    var devicesAttending = document.getElementsByClassName("hiddenDeviceNumber");
    for(var i = 0; i < devicesAttending.length; i++){
        allDevices.push(devicesAttending[i].value);
    }
    var deviceSections = document.getElementsByClassName("hiddenDeviceSectionName");
    for(var i = 0; i < deviceSections.length; i++){
        var split = deviceSections[i].value.split("_");
        var thisDevice = split[0];
        var thisSection = split[1];
        if(!(thisDevice in allDeviceSections)){
            allDeviceSections[thisDevice] = [];

        }
        allDeviceSections[thisDevice].push(thisSection);
    }
    for(var i = 0; i < allDevices.length; i++){
        for(var j = 0; j < allDeviceSections[allDevices[i]].length; j++){
            var thisDeviceSectionName = allDeviceSections[allDevices[i]][j];
            var thisDeviceSection = document.getElementById(allDevices[i].toString() + "" + thisDeviceSectionName);
            thisDeviceSection.style.display = "none";
        }
    }
    openDeviceSection(allDevices[0].toString(), allDeviceSections[allDevices[0]][0].toString());
    currentDevice = allDevices[0].toString()
}
function openDeviceSection(deviceNumber, sectionNumber){
    deviceSectionIndex = 0;
    var allDeviceSectionContainers = document.getElementsByClassName("hiddenSection");
    var allSectionsContainers = document.getElementsByClassName("hiddenDeviceSection");
    for(var i = 0; i < allSectionsContainers.length - 1; i++){
        var closing = allSectionsContainers[i];
        closing.style.display = "none";
    }
    for(var i = 0; i < allDeviceSectionContainers.length; i++){
        var thisDevice = allDeviceSectionContainers[i];
        thisDevice.style.display = "none";
    }
    var deviceName = deviceNumber.toString();
    var openingDevice = document.getElementById(deviceName);
    openingDevice.style.display = "block";
    console.log(openingDevice);
    currentDevice = deviceName;
    var sectionName = sectionNumber.toString();
    var elementOpening = document.getElementById(deviceName + "" + sectionName);
    console.log(elementOpening);
    elementOpening.style.display = "block";
}
function nextDeviceSection(){
    var thisDevice = currentDevice;
    var lastSectionName = "section" + deviceSectionIndex.toString();
    deviceSectionIndex++;
    console.log(allDeviceSections[thisDevice]);
    if(deviceSectionIndex > allDeviceSections[thisDevice].length - 1){
        deviceSectionIndex = 0;
    }
    if(allDeviceSections[thisDevice].length == 1){
        var lastSection = document.getElementById(thisDevice.toString() + "" + lastSectionName);
        lastSection.style.display = "block";
    } else {
        console.log(deviceSectionIndex);
        var newSectionName = "section" + deviceSectionIndex.toString();
        console.log(thisDevice);
        var nextSection = document.getElementById(thisDevice.toString() + "" + newSectionName);
        var lastSection = document.getElementById(thisDevice.toString() + "" + lastSectionName);
        nextSection.style.display = "block";
        lastSection.style.display = "none";
    }
}
function startPage(){
    setTimeout(getAllSections, 200);
}
startPage();
// var sectionIndex = 0;
// function openVideoSection(videoSection){
//     var sectionNumber = videoSection.slice(7);
//     sectionIndex = sectionNumber;
//     var allSectionContainers = document.getElementsByClassName("singleSectionContainer");
//     for(var i = 0; i < allSectionContainers.length; i++){
//         allSectionContainers[i].style.display = "none";
//     }
//     var openingContainer = document.getElementById(videoSection);
//     openingContainer.style.display = "table-row-group";
// }
// function nextVideoSection(){
//     sectionIndex++;
//     if(sectionIndex > allSections.length - 1){sectionIndex = 0};
//     var openingName = "section" + sectionIndex.toString();
//     openVideoSection(openingName);
// }
// function lastVideoSection(){
//     sectionIndex--;
//     if(sectionIndex < 0){sectionIndex = allSections.length - 1};
//     var openingName = "section" + sectionIndex.toString();
//     openVideoSection(openingName);
// }
// function openSectionButtons(){
//     var buttons = document.getElementById("sectionButtonHolder");
//     buttons.style.display = "table-row-group";
//   }
//   function closeSectionButtons(){
//     var buttons = document.getElementById("sectionButtonHolder");
//     buttons.style.display = "none";
//   }