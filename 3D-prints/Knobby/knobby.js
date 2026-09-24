/*

Knobby v2

Run in https://openjscad.xyz/v3/

Or install the JSCAD preview extension by Coding Wellin VSCode.

*/

const jscad = require('@jscad/modeling')

const { colorize } = require('@jscad/modeling').colors;
const { extrudeLinear } = require('@jscad/modeling').extrusions
const { union, intersect, scission, subtract } = require('@jscad/modeling').booleans
const { ellipsoid, cuboid, roundedCuboid, cylinder, polygon, cylinderElliptic } = jscad.primitives
const { rotate, rotateX, rotateY, rotateZ, translate, translateX, translateY, translateZ,  
        mirror, mirrorX, mirrorY, mirrorZ, scale} = require('@jscad/modeling').transforms
const { hull, hullChain } = require('@jscad/modeling').hulls;

//select output to print
// let whichToPrint = ['body', 'button', 'pot', 'esp', 'notch']
let whichToPrint = ['', 'body', '']

//CONSTANTS
const bodySize = [130,92,35]
const panelHeight = 4
const buttonSpacing = 32
const buttonPos = [[-buttonSpacing*1.5,-20,0],
  [-buttonSpacing*.5,-30,0],
  [buttonSpacing*.5,-30,0],
  [buttonSpacing*1.5,-20,0]
]
const potPos = [[buttonSpacing*1.5+5,10,0],
  [buttonSpacing*.5+19,25,0],
  [-buttonSpacing*.5-19,25,0],
  [-buttonSpacing*1.5-5,10,0]
]
const potAngle = Math.PI/2

const screwLength = 10
const espPos = [12,0,-screwLength-1]
const rotateESP = true

//MAIN FUNCTION *******************************************************
const main = (params) => {
  let body = roundedCube({size:bodySize, radius:10, center:[0,0,-bodySize[2]/2], bevel:4})

  body = shell({
    body: body,
    bodyDimensions: bodySize,
    topThickness: 4,
    wallThickness: 2
    })

   

  let button = [
    translate( buttonPos[0] ,makeButton()),
    translate( buttonPos[1] ,makeButton()),
    translate( buttonPos[2] ,makeButton()),
    translate( buttonPos[3] ,makeButton())
    ]
  let pot = [
    translate( potPos[0] , rotateZ(potAngle,makePot())),
    translate( potPos[1] , rotateZ(potAngle,makePot())),
    translate( potPos[2] , rotateZ(potAngle,makePot())),
    translate( potPos[3] , rotateZ(potAngle,makePot()))
    ]

  //ESP and standoffs
  let standoffs = translate( espPos ,makeStandoffs())
  if (rotateESP) standoffs = rotateZ(Math.PI/2, standoffs)
  body = union( body, standoffs )
  let esp = translate( espPos ,makeEsp())
  if (rotateESP) esp = rotateZ(Math.PI/2, esp)
  body = subtract( body, esp )
  body = subtract(body, [pot,button])

  let notch = makeNotch()
  body = subtract(body, notch)
  
  if( Array.isArray(whichToPrint)){
    let prints = []
    for(let i=0;i<whichToPrint.length;i++){
      switch (whichToPrint[i]){
        case "body": prints.push( body ); break;
        case "button": prints.push( button ); break;
        case "pot": prints.push( pot ); break;
        case "esp": prints.push( colorize([.2,.2,.5],esp) ); break;
        case "notch": prints.push( colorize([1,.2,.2],notch) ); break;
       }
    }
    return prints
  }
  
  return
}

/* MAKE FUNCTIONS *******************************************************
*********************************************************/

const makeBevel = ({ body, dimensions, amount = 4 }) => {
  // dimensions should be [width, length, height]
  // amount: vertical extent of the bevel
  
  // Top bevel at z=0
  let topBevel = roundedCube({
    size: [dimensions[0]*.1, dimensions[1]*0.1, 1],
    radius: 3,
    center: [0, 0, dimensions[0]/4]
  })
  
  // Bottom bevel - larger to create the transition slope
  let bottomBevel = roundedCube({
    size: [dimensions[0] * 2, dimensions[1] * 2, 1],
    radius: 3,
    center: [0, 0,  -dimensions[0]/4]
  })
  
  // Hull them together to create the bevel transition
  let bevelShape = hull(topBevel, bottomBevel)
  
  // Scale inward to create the bevel shell effect
  let bevelCut = scale([0.5, 0.5, 1], bevelShape)
  bevelShape = subtract(bevelShape, bevelCut)

  bevelShape = translateZ(dimensions[0]/4-amount, bevelShape) // Move down to create the bevel effect
  
  // Subtract from body to create the beveled edge
  // return [body,bevelShape]
  return subtract(body, bevelShape)
}

const makeButton = ()=>{
  let main = cylinder({radius:23.9/2, height:20, center:[0,0,-10+5]})
  let cut =  cylinder({radius:28/2, height:10,center:[0,0,-5-2]})
  let notch = cylinder({
    radius:4,
    height:20,
    center:[0,0,-10+5]
  })
  let top = ellipsoid({ radius: [25/2,25/2,10/2], segments: 64, center:[0,0,10/2] })
  let notches = [
    translate([6,6,0], notch),
    translate([6,-6,0], notch),
    translate([-6,6,0], notch),
    translate([-6,-6,0], notch),
  ]

  return union(main,cut, notches,top)
}

const makePot = ()=>{ 
  let main = cylinder({radius:7/2, height:20}) //shaft
  let body = cylinder({radius:17/2, height:9, center:[0,0,-8]})
  body = union(body, cuboid({size:[18,15,9], center:[18/2,0,-8]}))
  let tab = cuboid({size:[3,3,8], center:[0,-7,0]})

  let knob = cylinder({radius:12, height:20, center:[0,0,10+2]}) //shaft
  return union(main, body,tab, knob)
}

const makeEsp = ()=>{
  let body = cuboid({size:[58.5,50.8,2], center:[0,0,0]})
  
  //screws with chamfer near PCB
  let main = []
  let holes = [
    [53.34/2,45.72/2],
    [-53.34/2,45.72/2],
    [53.34/2,-45.72/2],
    [-53.34/2,-45.72/2]
  ]
  holes.forEach(([x, y]) => {
    let hole = cylinder({radius:3/2, height:screwLength-1, center:[x,y,screwLength/2]})
    let chamfr = cylinderElliptic({height: 2, startRadius: [3,3], endRadius: [1,1], segments: 64, center:[x,y,2]})
    hole = union(hole, chamfr)
    main.push( hole)
  })

  //hole for usb cable
  let usbHole = cylinder({radius:10/2, height:80})
  usbHole = rotateY(Math.PI/2, usbHole)
  usbHole = translate([40,3,-30/2-2], usbHole)

  return union( body, main, usbHole )
}

const makeStandoffs = ()=>{
  let standoffHeight = screwLength
  let main = []
  let holes = [
    [53.34/2,45.72/2],
    [-53.34/2,45.72/2],
    [53.34/2,-45.72/2],
    [-53.34/2,-45.72/2]
  ]
  holes.forEach(([x, y]) => {
    let standoff = cylinderElliptic({height: standoffHeight, startRadius: [3,3], endRadius: [4,4], segments: 64, center:[x,y,standoffHeight/2+1]})
    main.push( union( standoff))
  })
  return union( main )
}

const makeNotch = ()=>{
  let notch = cylinder({radius:5, height:10})
  notch = rotateY(Math.PI/2, notch)
  notch = [
    translate([bodySize[0]/2,bodySize[1]/2+-20,-15], notch),
    translate([-bodySize[0]/2,bodySize[1]/2+-20,-15], notch),
    
  ]
  return notch
}


/* UTILITIES *******************************************************
*********************************************************/

const pattern = (object, offset = 10)=>{
  let obj = [object, translateY(10,object), translateY(-10,object)]
  return obj
}

const patternWide = (object, Yoffset = 18, Xoffset = 18)=>{
  let obj = [object, translateY(Yoffset,object), translateY(-Yoffset,object)]
  return union( obj, patternOffset(object, Yoffset, Xoffset))
}

const patternWideInline = (object, offset = 18)=>{
  let obj = [object, translateY(offset,object), translateY(-offset,object)]
  return union( obj, patternOffset(object, offset))
}

const patternOffset = (object, Yoffset = 18, Xoffset = 12)=>{
  let obj = [translateY(Yoffset/2,object), translateY(-Yoffset/2,object)]
  obj = translateX(Xoffset, obj)
  return obj
}

const offsetOne = (object, Yoffset = 18, Xoffset = 12)=>{
  let obj = [translateY(Yoffset/2,object)]
  obj = translateX(Xoffset, obj)
  return obj
}

const shell = ({ body, bodyDimensions, topThickness = 1, wallThickness = 1 }) => {
  const innerDim = bodyDimensions.map(x => x - wallThickness * 2)

  const scaleFactors = bodyDimensions.map((x, i) => innerDim[i] / x)
  let cut = scale(scaleFactors, body)
  cut = translateZ(-topThickness, cut)
  return subtract(body, cut)
}


const roundedCube = ({ size = [10, 10, 10], radius = 1, center = [0,0,0], bevel = 0 }) => {
    
    //make main body
    let edges = [];
    for (let i = 0; i < 4; i++) {
        let x = size[0] / 2 - radius;
        if (i > 1) x = -x;
        let y = size[1] / 2 - radius;
        if (i % 2 == 1) y = -y;

        // Place cylinder at (x, y), extruded vertically
        edges.push(
            translate([x, y, 0],
                cylinder({
                    height: size[2]-bevel,
                    radius: radius,
                    segments: 128
                })
            )
        );
    }
    let mainBody = hull(edges);

    if( bevel > 0 ){
    //make top for beveling
    edges = [];
    for (let i = 0; i < 4; i++) {
        let x = size[0] / 2 - radius - bevel/2;
        if (i > 1) x = -x;
        let y = size[1] / 2 - radius - bevel/2;
        if (i % 2 == 1) y = -y;

        // Place cylinder at (x, y), extruded vertically
        edges.push(
            translate([x, y, 0],
                cylinder({
                    height: bevel,
                    radius: radius,
                    segments: 128
                })
            )
        );
    }
    let top =  hull(edges);
    top = translateZ(size[2]/2-bevel/2, top)
    mainBody = translateZ(-bevel/2, mainBody)
    mainBody = hull(mainBody, top);
  }

    mainBody = translate(center, mainBody)

    return mainBody;
}

module.exports = { main }